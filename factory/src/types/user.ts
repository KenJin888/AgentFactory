export interface User {
  id: number;
  name: string;
  username?: string;
  mobile?: string;
  dept_id?: number;
  dept_name?: string;
  dept?: { id: number; name: string };
}

export interface Dept {
  id: number;
  name: string;
  children?: Dept[];
}
