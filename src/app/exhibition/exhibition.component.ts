import { Component, OnInit } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-exhibition',
  templateUrl: './exhibition.component.html',
  styleUrls: ['./exhibition.component.scss']
})
export class ExhibitionComponent implements OnInit {

  data !: any[]
  tab: number = 0

  constructor() { }

  changeTab(tab: number) {
    this.data = []
    this.tab = tab;
    axios({
      url: "http://localhost:3000/exhibition/"+(this.tab+1),
    }).then(res => {this.data = (res.data as any).data as any[]})
  }

  ngOnInit(): void {
    axios({
      url: "http://localhost:3000/exhibition/"+(this.tab+1),
    }).then(res => {this.data = (res.data as any).data as any[]})
  }

}
