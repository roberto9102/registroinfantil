import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  imports: [],
  selector: 'app-vacunas',
  styleUrl: './vacunas.component.css',
  templateUrl: './vacunas.component.html',
})
export class VacunasComponent {

  vacunas: any[] = [];

  constructor(private http: HttpClient) {}
  
    ngOnInit() {
    this.http.get<any[]>(
      'http://127.0.0.1:8000/api/vacunas/'
    ).subscribe(data => {
      this.vacunas = data;
    });
  }
}
