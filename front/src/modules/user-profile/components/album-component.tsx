import React, {useState, useEffect} from 'react';
import {Container} from '@material-ui/core';
import {IAlbum} from 'app/shared/model/album.model';
import AlbumItem from 'app/modules/user-profile/components/album-item';

interface IAlbumProps {
	title: string,
	data : IAlbum[]
}

const AlbumComponent = (props: IAlbumProps) => {
	return (
		<Container maxWidth="xl">
			{props.data.map( (item:IAlbum, index:number) => 
				<AlbumItem
					key={String(index)}
					album={item}
					hasCategories={true}
					hasTags={true}
				/>
					
				)}
		</Container>
	)
}

export default AlbumComponent;
