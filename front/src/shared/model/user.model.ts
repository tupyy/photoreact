export interface IUser {
  id?: any;
  active?: boolean,
  username?: string;
  firstName?: string;
  lastName?: string;
  email?: string;
  roles?: any[];
  langKey: string;
  password?: string;
}

export const defaultValue: Readonly<IUser> = {
  id: '',
  active: false,
  username: '',
  firstName: '',
  lastName: '',
  email: '',
  langKey: '',
  roles: [],
  password: ''
};
