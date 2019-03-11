import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { TreeComponent } from './tree/tree.component';
import { BranchDetailComponent } from './branch-detail/branch-detail.component';
import { AuthModule } from './auth/auth.module';

import { BranchService } from './branch.service';
import { AppRoutingModule } from './app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { BranchSearchComponent } from './branch-search/branch-search.component';
import { BranchesListComponent } from './branches-list/branches-list.component';
import { BranchFormComponent } from './branch-form/branch-form.component';
import { FeatureFormFieldsetComponent } from './feature-form-fieldset/feature-form-fieldset.component';


@NgModule({
  declarations: [
    AppComponent,
    TreeComponent,
    BranchDetailComponent,
    DashboardComponent,
    BranchSearchComponent,
    BranchesListComponent,
    BranchFormComponent,
    FeatureFormFieldsetComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    AuthModule
  ],
  providers: [ BranchService ],
  bootstrap: [AppComponent]
})
export class AppModule { }
