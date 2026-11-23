import { Routes } from '@angular/router';
import { MenuComponent } from './pages/menu/menu.component';
import { VacunasComponent } from './pages/vacunas/vacunas.component';

export const routes: Routes = [
    {path: '',component: MenuComponent},
    {path: 'vacunas',component: VacunasComponent}
];
