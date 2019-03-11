import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }   from './dashboard/dashboard.component';
import { TreeComponent }      from './tree/tree.component';

import { AuthGuard }            from './auth/auth-guard.service';
import { AuthService }          from './auth/auth.service';
import { LoginComponent }       from './auth/login/login.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },

  { path: '', redirectTo: '/dashboard', pathMatch: 'full'},
  { path: 'dashboard', component: DashboardComponent,
    // canActivate: [AuthGuard]
  },
  { path: 'tree', component: TreeComponent,
    // canActivate: [AuthGuard] 
  }
];

@NgModule({
  exports: [
      RouterModule
  ],
  imports: [
      RouterModule.forRoot(routes)
  ],
  providers: [
    AuthGuard,
    AuthService
  ]
})
export class AppRoutingModule {}
