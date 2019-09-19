import {IAlbum} from 'app/shared/model/album.model';

export interface IContentObjectLog {
	id: number,
	name: string,
	type: string
}

export interface IPermissionLog {
	contentObject: IContentObjectLog,
	userFrom: string,
	album: IAlbum,
	date: Date,
	permission: string,
	action: string
}

export const getPermissionLogMockingData = (): IPermissionLog[] => {
	let arr: IPermissionLog[];
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
			date: new Date('2019-01-01T00:00:00'),
			preview: "link"
		},
		permission: "add_photos",
		date: new Date('2019-01-01T:00.00:00'),
		action: "add"
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
			date: new Date('2019-01-01T00:00:00'),
			preview: "link"
		},
		permission: 'change_album',
		date: new Date('2019-01-01T:00.00:00'),
		action: "modifiy"
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
			date: new Date('2019-01-01T00:00:00'),
			preview: "link"
		},
		permission: 'add_photos',
		date: new Date('2019-01-01T:00.00:00'),
		action: "delete"
	});
	return arr;
}

