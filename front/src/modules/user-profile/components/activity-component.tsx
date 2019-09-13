import React, {useState, useEffect} from 'react';
import axios from 'axios';
import { Container } from '@material-ui/core';
import ActivityItem from './activity-item';
import {IActivity} from 'app/shared/model/activity.model';

interface IActivityComponent {
    url: string,
    title: string,
}

/**
 * It renders the activities fetched from server. It can be embedded into Overview or Activities tabs
 */
const ActivityComponent = (props: IActivityComponent) => {
    const [data, setData] = useState([]);
    const [error, setError] = useState(null);

    useEffect( () => {
        const fetchData = async (url: string) => {
            try {
                const response = await axios.get(url);
                if (response) {
                    setData(response.data.results);
                }
            } catch (error) {
                setError(error);
            }
        }
        fetchData(props.url);
    }, []);

    return (
        <Container maxWidth="xl">
            {data.map( (item: IActivity, index: number ) => 
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