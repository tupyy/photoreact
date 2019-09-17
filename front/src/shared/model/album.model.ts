export interface IAlbum {
    id: number,
    name?: string,
    description?: string,
    date: Date,
    preview: string,
    categories?: string[],
    tags?: string[]
}

export const defaultValue: Readonly<IAlbum> = {
    id: -1,
    name: '',
    description: '',
    date: new Date(),
    preview: '',
    categories: [],
    tags: [] 
}
