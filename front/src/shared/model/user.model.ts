export interface IUser {
  id?: any;
  username?: string;
  firstName?: string;
  lastName?: string;
  email?: string;
  roles?: any[];
  password?: string;
}

export const defaultValue: Readonly<IUser> = {
  id: '',
  username: '',
  firstName: '',
  lastName: '',
  email: '',
  roles: [],
  password: ''
};
