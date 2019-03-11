import { Component, EventEmitter, OnInit, Input, Output, ViewChild } from '@angular/core';
import { Branch } from '../branch';
import { BranchService } from '../branch.service';

@Component({
  selector: 'app-branches-list',
  templateUrl: './branches-list.component.html',
  styleUrls: ['./branches-list.component.css']
})
export class BranchesListComponent implements OnInit {

    private _branches: Branch[];
    get branches(): Branch[] { return this._branches; }
    set branches(branches: Branch[]) { this._branches = branches; this.selectedBranch = undefined; }

    @Output()
    onAddBranch = new EventEmitter<Branch>();

    @Output()
    onBranchesShowed = new EventEmitter<void>();

    private _parent_branch: Branch;

    @Input()
    set parent_branch(branch: Branch) {
        this._parent_branch = branch;
        this.getBranches();
    }
    get parent_branch(): Branch { return this._parent_branch; }

    constructor(private branchService: BranchService) { }

    selectedBranch: Branch;

    @Output()
    onBranchSelected = new EventEmitter<Branch>();
    onSelect(branch: Branch): void {
      this.selectedBranch = branch;
      this.onBranchSelected.emit(branch);
    }

    ngOnInit() {
        this.getBranches();
    }
    getBranches(): void {
        this.branchService.getBranches(this.parent_branch)
            .subscribe(branches => this.displayBranches(branches));
    }
    displayBranches(branches: Branch[]): void {
        if(this.parent_branch){
            for(var i=0;i<branches.length;i++){
                branches[i]["parent"] = this.parent_branch;
            }
        }
        this.branches = branches;
        this.onBranchesShowed.emit();
    }
}
