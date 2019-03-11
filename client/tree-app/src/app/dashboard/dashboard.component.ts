import { Component, OnInit } from '@angular/core';
import { Branch } from '../branch';
import { BranchService } from '../branch.service';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
  branches: Branch[] = [];

  constructor(
    private branchService: BranchService
  ) { }

  ngOnInit() {
    this.getBranches();
  }

  getBranches(): void {
    this.branchService.getBranches(undefined)
      .subscribe(branches => this.branches = branches.slice(1, 5));
  }
}
