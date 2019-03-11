import { Component, OnInit, Input } from '@angular/core';
import { Feature } from '../branch';

@Component({
  selector: 'app-feature-form-fieldset',
  templateUrl: './feature-form-fieldset.component.html',
  styleUrls: ['./feature-form-fieldset.component.css']
})
export class FeatureFormFieldsetComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  @Input()
  feature: Feature;

}
