export class Feature {
    name: string;
    representation: string;
    choices: string[];
}

export class Branch {
  id: string;
  name: string;
  description: string = "";

  parent_id: string = undefined;
  parent: Branch = undefined;

  features: Feature[];
}
