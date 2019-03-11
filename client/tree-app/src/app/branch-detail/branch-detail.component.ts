import { Component, OnInit, Input, Output, EventEmitter, ElementRef  } from '@angular/core';
import { Branch } from '../branch';

import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { BranchService } from '../branch.service';

@Component({
  selector: 'app-branch-detail',
  templateUrl: './branch-detail.component.html',
  styleUrls: ['./branch-detail.component.css']
})
export class BranchDetailComponent implements OnInit {

    private _operation: string = "preview";

    @Input()
    set operation(operation: string) {
        this._operation = operation;
    }
    get operation(): string { return this._operation; }

    private _selected_branch: Branch;

    @Input()
    set selected_branch(branch: Branch) {
        this._selected_branch = branch;
        this.branch = branch;
    }
    get selected_branch(): Branch { return this._selected_branch; }

    branch: Branch;

    @Output()
    editBranch = new EventEmitter<void>();

    // event to TreeComponent
    @Output()
    askRefreshTree = new EventEmitter<any>();
    @Output()
    scrollToBranchList = new EventEmitter<void>();
    @Output()
    scrollToDetails = new EventEmitter<void>();

    constructor(
        private route: ActivatedRoute,
        private branchService: BranchService,
        public el: ElementRef
    ) {}

    ngOnInit(): void {
        this.branch = this.selected_branch;
    }

    addBranch(parent: Branch) {
        this.branch = new Branch();
        if(parent){
            this.branch["parent_id"] = parent.id;
        }
        this.operation = "add";
    }
    saveBranch(branch: Branch){
        if(this.operation == "add"){
            this.branchService.addBranch(branch)
              .subscribe(result => this.handleResult(result));
        }else if(this.operation == "edit"){
            console.log(branch);
            this.branchService.updateBranch(branch)
                .subscribe(result => this.handleResult(result));
        }
    }
    handleResult(result: any): void {
        console.log("result");
        console.log(result);
        console.log(typeof result);
        this.branch = result;
        this.operation = "preview";
        this.askRefreshTree.emit(undefined);
    }
}
