import { writable } from 'svelte/store';

// For storing the bot's reply
export const botReplyStore = writable<string>("");

// For storing the user's request
export const userRequestStore = writable<string>("");

// For storing isLoading which is used for the loading icon
export const isLoadingStore = writable<boolean>(false);