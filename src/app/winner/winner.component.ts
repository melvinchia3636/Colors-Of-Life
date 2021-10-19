import { Component, OnInit } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-winner',
  templateUrl: './winner.component.html',
  styleUrls: ['./winner.component.scss']
})
export class WinnerComponent implements OnInit {

  data !: any[];
  groupTab: number = 0;
  categoryTab: number = 0;

  constructor() { }

  fetchData() {
    axios({
      url: `http://localhost:3000/winner/${this.groupTab}/${this.categoryTab}`,
    }).then(res => {this.data = (res.data as any).data as any[]});
  }

  changeGroupTab(tab: number) {
    this.data = [];
    this.groupTab = tab;
    this.fetchData();
  }

  changeCategoryTab(tab: number) {
    this.data = [];
    this.categoryTab = tab;
    this.fetchData();
  }

  ngOnInit(): void {
    this.fetchData();
  }

}
