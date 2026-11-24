import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class Auth {
    
    constructor(private http: HttpClient) {}
    
    login(username: string, password: string) {
    return this.http.post<TokenPair>(
        'http://127.0.0.1:8000/api/token/',
        {
            username,
            password
        }
    );
}
    guardarTokens(tokens: TokenPair) {
    sessionStorage.setItem('access', tokens.access);
    sessionStorage.setItem('refresh', tokens.refresh);
    }

    obtenerAccess(): string | null {
    return sessionStorage.getItem('access');
    }

    logout() {
    sessionStorage.removeItem('access');
    sessionStorage.removeItem('refresh');
    }
}

export interface TokenPair {
  access: string;
  refresh: string;
}

