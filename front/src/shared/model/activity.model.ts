export interface IActivity {
    content_object: {
        id: number,
        name: string,
        type: string,
        link: string
    },
    user: string,
    date: string,
    activity: string
}