import React from 'react';
import {IPermissionLog} from 'app/shared/model/permission_log.model';
import {Container} from '@material-ui/core';
import PermissionLogItem from 'app/modules/user-profile/components/permission-log-item';

export interface IPermissionComponent {
	title: string,
	data: IPermissionLog[]
}

const PermissionComponent = (props: IPermissionComponent) => {
	return (
		<Container maxWidth="xl">
			{props.data.map( (item:IPermissionLog, index:number) => 
				<PermissionLogItem 
					key={index.toString()}
					permissionLog={item}
				/>
				)}
		</Container>
	)
};


export default PermissionComponent;

