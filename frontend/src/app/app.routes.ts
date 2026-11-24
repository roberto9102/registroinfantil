import { Routes } from '@angular/router';
import { MenuComponent } from './pages/menu/menu.component';
import { VacunasComponent } from './pages/vacunas/vacunas.component';
import { LoginComponent } from './pages/login/login.component';

export const routes: Routes = [
    {path: 'menu',component: MenuComponent},
    {path: '',component: LoginComponent},
    {path: 'vacunas',component: VacunasComponent}
];
