import { Component, OnInit, Input, Output, EventEmitter, ViewChild } from '@angular/core';
import { Branch, Feature } from '../branch';

@Component({
  selector: 'app-branch-form',
  templateUrl: './branch-form.component.html',
  styleUrls: ['./branch-form.component.css']
})
export class BranchFormComponent implements OnInit {
  constructor() {}
  ngOnInit() {}

  @Input()
  selected_branch: Branch;
  initial_branch: Branch;
  branch: Branch = new Branch();
  setBranch(branch: Branch){
      this.initial_branch = branch;
      this.branch = Object.assign({}, branch);
  }
  applyBranch(){
      this.initial_branch = Object.assign(this.initial_branch, this.branch);
      this.onFormSubmit.emit(this.branch);
  }

  // events to DetailComponent
  @Output()
  onFormSubmit = new EventEmitter<Branch>();
  @Output()
  onCancel = new EventEmitter<void>();

  // events to TreeComponent
  @Output()
  askRefreshTree = new EventEmitter<any>();
  @Output()
  scrollToBranchList = new EventEmitter<void>();
  @Output()
  scrollToDetails = new EventEmitter<void>();

  @ViewChild('detailsFieldset')
  private details_fieldset: any;
  parent_selecting: boolean = false;
  startSelectingParent(){
      this.askRefreshTree.emit(undefined);
      this.parent_selecting = true;
      this.details_fieldset.nativeElement.disabled = true;
      this.scrollToBranchList.emit();
  }
  stopSelectingParent(){
      this.parent_selecting = false;
      this.details_fieldset.nativeElement.disabled = false;
      this.scrollToDetails.emit();
  }
  applySelectedParent(){
      this.branch.parent = this.selected_branch;
      this.branch.parent_id = this.selected_branch.id;
      this.stopSelectingParent();
  }
  dropParent(){
      this.branch.parent = undefined;
  }

  pushFeature(){
      let feature = new Feature();
      this.branch.features.push(feature);
      console.log(this.branch);
  }
}
