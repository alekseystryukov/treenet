import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { Branch } from '../branch';
import {BranchDetailComponent } from '../branch-detail/branch-detail.component';
import { BranchesListComponent } from '../branches-list/branches-list.component';


@Component({
  selector: 'app-tree',
  templateUrl: './tree.component.html',
  styleUrls: ['./tree.component.css']
})
export class TreeComponent implements OnInit {

  constructor() { }

  ngOnInit() {}

  selectedBranch: Branch;

  onBranchSelected(branch: Branch){
      this.selectedBranch = branch;
  }

  onBranchesShowed(){
      this.scrollToRight();
  }

  @ViewChild('treeSlider')
  private slider: any;

  scrollToRight(){
      this.slider.nativeElement.scrollLeft = this.slider.nativeElement.scrollWidth;
  }

  @ViewChild('branchDetail')
  private branch_detail_component: BranchDetailComponent;

  addBranch(parent: Branch){
      this.branch_detail_component.addBranch(parent);
      this.scrollToDetails();
  }

  @ViewChild('branchesTopList')
  private branches_list_component: BranchesListComponent;

  refreshTree(branch_id: any){
      console.log("show branch " + branch_id);
      this.branches_list_component.selectedBranch = undefined;
      this.branches_list_component.getBranches();
  }
  scrollToBranchList(){
      window.scrollTo(0, this.slider.nativeElement.offsetTop);
  }
  scrollToDetails(){
      window.scrollTo(0, this.branch_detail_component.el.nativeElement.offsetTop);
  }

}
