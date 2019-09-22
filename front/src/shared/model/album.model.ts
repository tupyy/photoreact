import {IUser} from 'app/shared/model/user.model';

export interface IAlbum {
    id: number,
	owner: IUser,
    name?: string,
    description?: string,
    date: Date,
    preview: string,
    categories?: string[],
    tags?: string[]
	isFavorite: boolean
}

