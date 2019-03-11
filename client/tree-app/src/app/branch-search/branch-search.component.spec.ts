import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BranchSearchComponent } from './branch-search.component';

describe('BranchSearchComponent', () => {
  let component: BranchSearchComponent;
  let fixture: ComponentFixture<BranchSearchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BranchSearchComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BranchSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
