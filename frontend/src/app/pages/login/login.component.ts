import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import { Auth } from '../../services/auth';
import { Router } from '@angular/router';

@Component({
  imports: [FormsModule],
  selector: 'app-login',
  styleUrl: './login.component.css',
  templateUrl: './login.component.html',
})
export class LoginComponent {

 constructor( private Auth: Auth,private Router: Router) {}
  
    username = '';
    password = '';
    mensajeError = '';
  iniciarSesion() {

  this.Auth.login(
    this.username,
    this.password
  ).subscribe({
    next: (tokens) => {
      this.Auth.guardarTokens(tokens)
      this.Router.navigate(['/vacunas'])
    },

    error: (error) => {
      this.mensajeError = 'Credenciales incorrectas';
    }

  });
}
}
