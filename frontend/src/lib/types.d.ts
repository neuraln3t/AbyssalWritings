type StoryPreview = {
    uuid: string;
    title: string;
    content: string;
    image: string;
    date: string;

    hearts: number;
};

export type User = {
    loggedIn: boolean;
    username: string;
    date_joined: string;
    
    avatar: UserAvatar;
}

export type UserAvatar = {
    uuid: string;
    image: string;
}

export type Tokens = {
    refresh: string;
    access: string;
}

type StoryComment = {
    user: User;

    text: string;
    date: string;
}

export type Story = {
    uuid: string;
    title: string;
    content: string;
    date: string;
    
    image: string;
    comments: Array<StoryComment>;
    genre: Genre;

    active: boolean;
    liked: boolean;

    hearts: number;
}

export type Genre = {
    uuid: string;
    name: string;
    description: string;
    banner: string;
}

export type StoryLine = {
    uuid: string;
    title: string;
    description: string;
    
    stories: Array<Story>
}