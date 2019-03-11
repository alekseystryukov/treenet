import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthGuard } from './auth-guard.service';
import { AuthService } from './auth.service';
import { LoginComponent } from './login/login.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [
      LoginComponent
  ],
  exports: [
      LoginComponent
  ],
  providers: [AuthGuard, AuthService]
})
export class AuthModule { }
