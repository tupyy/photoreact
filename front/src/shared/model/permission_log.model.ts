import {IAlbum} from 'app/shared/model/album.model';
import moment from 'moment';

export interface IContentObjectLog {
	id: number,
	name: string,
	type: string
}

export interface IPermissionLog {
	contentObject: IContentObjectLog,
	userFrom: string,
	album: IAlbum,
	date: string,
	permission: string,
	operation: string
}

export const getPermissionLogMockingData = (): IPermissionLog[] => {
	let arr: IPermissionLog[] = [];
	arr.push({
		contentObject: {
			id: 1,
			name: "Toto titi",
			type: "user"
		},
		userFrom: "admin",
		album: {
			id: 1,
			name: "album1",
			date:"dd", 
			preview: "link"
		},
		permission: "add_photos",
		date: moment().format('DD/MM/YYYY'),
		operation: "add"
	});

	arr.push({
		contentObject: {
			id: 2,
			name: "user2",
			type: "user"
		},
		userFrom: "admin",
		album: {
			id: 2,
			name: "album2",
			date: new Date('2019-01-01T00:00:00Z'),
			preview: "link"
		},
		permission: 'change_album',
		date: moment().format('DD/MM/YYYY'),
		operation: "modify"
	});

	arr.push({
		contentObject: {
			id: 1,
			name: "user1",
			type: "user"
		},
		userFrom: "admin",
		album: {
			id: 1,
			name: "album1",
			date: new Date('2019-01-01T00:00:00Z'),
			preview: "link"
		},
		permission: 'add_photos',
		date: moment().format('DD/MM/YYYY'),
		operation: "delete"
	});
	return arr;
}

