import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FeatureFormFieldsetComponent } from './feature-form-fieldset.component';

describe('FeatureFormFieldsetComponent', () => {
  let component: FeatureFormFieldsetComponent;
  let fixture: ComponentFixture<FeatureFormFieldsetComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FeatureFormFieldsetComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FeatureFormFieldsetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
