import {IAlbum} from 'app/shared/model/album.model';
import {IUser} from 'app/shared/model/user.model';

export interface IContentObjectLog {
	id: number,
	name?: string,
	profile?: IUser,
	type: string
}

export interface IPermissionLog {
	content_object: IContentObjectLog,
	userFrom: string,
	album: IAlbum,
	date: string,
	permission: string,
	operation: string
}

