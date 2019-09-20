import React from 'react';
import {IPermissionLog} from 'app/shared/model/permission_log.model';
import {Container} from '@material-ui/core';
import PermissionLogItem from 'app/modules/user-profile/components/permission-log-item';
import NoData from 'app/shared/components/no-data/no-data';

export interface IPermissionComponent {
	title: string,
	data: IPermissionLog[]
}

const PermissionComponent = (props: IPermissionComponent) => {
	const renderItems = (arr: IPermissionLog[]) => {
		return (
			arr.map( (item:IPermissionLog, index:number) => 
				<PermissionLogItem 
					key={index.toString()}
					permissionLog={item}
				/>
			))
	}

	return (
		<Container maxWidth="xl">
			{props.data.length > 0 ? (renderItems(props.data)) : (<NoData />)}
		</Container>
	)
};


export default PermissionComponent;

