import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {

  name !: any;

  constructor(private router: Router) { 
  }

  ngOnInit(): void {
    this.router.events.subscribe(
      (event: any) => {
        if (event instanceof NavigationEnd) {
          this.name = this.router.url;
        }
      }
    );
  }

}
