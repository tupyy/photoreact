import React, {useContext} from 'react';
import {ITabComponent} from "app/modules/user-profile/tab-component-interface";
import {TabContext} from "app/modules/user-profile/tab-context";
import {makeStyles, Theme} from "@material-ui/core";
import combineStyles from "app/shared/util/combine-styles";
import useTabComponentStyles from "app/modules/user-profile/components/tab-component-styles";

interface IPermissionsTab extends ITabComponent {

}

const useStyles = combineStyles(useTabComponentStyles,makeStyles( (theme: Theme) => {

}));

const PermissionsTab: React.SFC<IPermissionsTab> = (props: IPermissionsTab) => {

    const tabContext = useContext(TabContext);

    // @ts-ignore
    const classes = useStyles();
    return (
        <div className={props.index !== tabContext ? classes.hidden : classes.root}>
            Permissions component
        </div>
    )
};

export default PermissionsTab;
