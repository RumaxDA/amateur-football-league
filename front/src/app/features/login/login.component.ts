import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { SessionService } from '../../services/session.service';

export interface FormField {
  email: string;
  password: string;
}
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(
    private authService: AuthService,
    private router: Router,
    private sessionService: SessionService,
  ) {}

  login(): void {
    if (!this.email || !this.password) {
      this.errorMessage = 'Email and password are required';
      return;
    }

    this.authService
      .login(this.email, this.password)
      .pipe(
        catchError((error) => {
          console.error('Error:', error);
          if (error.status === 401) {
            this.errorMessage = 'Invalid email or password';
          } else {
            this.errorMessage = 'Invalid email or password';
          }
          return throwError(error);
        }),
      )
      .subscribe((response) => {
        if (response && response.access_token) {
          this.router.navigate(['/home']);
          const userId = this.sessionService.getUserId();
          if (userId) {
          }
        } else {
          this.errorMessage = 'Invalid email or password';
        }
      });
  }

  register(): void {
    this.router.navigate(['/register']);
  }
}
