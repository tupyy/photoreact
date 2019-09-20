import React, {useState} from 'react';
import {makeStyles, Paper, Tab, Tabs, Theme} from '@material-ui/core';

interface IUserProfileTabs {
    tabNames: string[],
    handleChange(value): void
}

const useStyles = makeStyles((theme: Theme) => ({
    root: {
        display: 'flex',
        justifyContent: 'center'
    },
    tab: {
        fontSize: '0.875rem',
        [theme.breakpoints.only('xs')]: {
            fontSize: '0.75rem'
        }
    }
}));

const UserProfileTabs = (props: IUserProfileTabs) => {
    const [value, setValue] = useState(0);

    const handleChange = (event: React.ChangeEvent<{}>, newValue: number) => {
        setValue(newValue);
        props.handleChange(newValue);
    };

    // @ts-ignore
    const classes = useStyles();

    return (
        <Paper square className={classes.root}>
            <Tabs
                value={value}
                indicatorColor="primary"
                textColor="primary"
                onChange={handleChange}
                aria-label="user-profile-tab"
            >
                {props.tabNames.map((tabName, index) =>
                    <Tab
                        key={String(index)}
                        label={tabName}
                        className={classes.tab}
                    />
                )}
            </Tabs>
        </Paper>
    )
};

export default UserProfileTabs;
