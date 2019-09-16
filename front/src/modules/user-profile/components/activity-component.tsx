import React from 'react';
import { Container } from '@material-ui/core';
import ActivityItem from './activity-item';
import {IActivity} from 'app/shared/model/activity.model';

export interface IActivityComponent {
    title: string,
	data: IActivity[]
}

/**
 * It renders the activities fetched from server. It can be embedded into Overview or Activities tabs
 */
const ActivityComponent = (props: IActivityComponent) => {
    return (
        <Container maxWidth="xl">
            {props.data.map( (item: IActivity, index: number ) => 
                <ActivityItem 
                    key={String(index)}
                    id={item.content_object.id}
                    title={item.content_object.name}
                    date={item.date}
                    activity={item.activity}
                    user={item.user}
                />
            )}
        </Container>
    )
};

export default ActivityComponent;
