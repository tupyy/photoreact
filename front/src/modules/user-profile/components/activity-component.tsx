import React from 'react';
import { Container } from '@material-ui/core';
import ActivityItem from './activity-item';
import {IActivity} from 'app/shared/model/activity.model';
import NoData from 'app/shared/components/no-data/no-data';

export interface IActivityComponent {
    title: string,
	data: IActivity[]
}

/**
 * It renders the activities fetched from server. It can be embedded into Overview or Activities tabs
 */
const ActivityComponent = (props: IActivityComponent) => {

	const renderItems = (arr: IActivity[]) => {
		return (
            arr.map( (item: IActivity, index: number ) => 
                <ActivityItem 
                    key={String(index)}
                    id={item.content_object.id}
                    title={item.content_object.name}
                    date={item.date}
                    activity={item.activity}
                    user={item.user}
                />
		   ))
	}

    return (
        <Container maxWidth="xl">
			{props.data.length > 0 ? (renderItems(props.data)) : (<NoData />)}
        </Container>
    )
};

export default ActivityComponent;
