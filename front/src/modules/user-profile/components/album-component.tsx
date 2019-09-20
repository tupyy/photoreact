import React from 'react';
import {Container} from '@material-ui/core';
import {IAlbum} from 'app/shared/model/album.model';
import AlbumItem from 'app/modules/user-profile/components/album-item';
import NoData from 'app/shared/components/no-data/no-data';

interface IAlbumProps {
	title: string,
	data : IAlbum[]
}

const AlbumComponent = (props: IAlbumProps) => {

	const renderItems = (arr: Array<IAlbum>) => {
		return (
			arr.map( (item:IAlbum, index:number) => 
				<AlbumItem
					key={index.toString()}
					album={item}
					hasCategories={true}
					hasTags={true}
				/>
		   ));
	}

	return (
		<Container maxWidth="xl">
			{props.data.length > 0 ? (
				renderItems(props.data)
			) : (
				<NoData />
			)}
		</Container>
	)
}

export default AlbumComponent;
