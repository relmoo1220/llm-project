<script lang="ts">
  import { onDestroy } from "svelte";
  import BotReply from "../components/BotReply.svelte";
  import SectionWrapper from "../components/SectionWrapper.svelte";
  import UserRequest from "../components/UserRequest.svelte";
  import {
    botReplyStore,
    isLoadingStore,
    userRequestStore,
  } from "../stores/globalStores";

  const apiUrl = "http://127.0.0.1:5000";

  let isLoading: boolean;
  let userRequest: string;
  let botReply: string;

  const unsubscribeBotReplyStore = botReplyStore.subscribe((value) => {
    botReply = value;
  });

  const unsubscribeUserRequestStore = userRequestStore.subscribe((value) => {
    userRequest = value;
  });

  const unsubscribeIsLoadingStore = isLoadingStore.subscribe((value) => {
    isLoading = value;
  });

  // Cleanup the subscription on component destruction
  onDestroy(() => {
    unsubscribeBotReplyStore();
    unsubscribeUserRequestStore();
    unsubscribeIsLoadingStore();
  });

  async function sendMessage() {
    try {
      isLoading = true;
      const response = await fetch(apiUrl + "/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: userRequest }),
      });

      // Check if the response is OK (status code 200)
      if (!response.ok) {
        isLoading = false;
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }

      // Parse the JSON response
      const data = await response.json();
      console.log("API Response:", data);
      botReplyStore.set(data.response);
      isLoading = false;
    } catch (error) {
      isLoading = false;
      console.error("Error fetching data from Flask API:", error);
    }
  }
</script>

<div class="bg-gray-700 flex flex-col justify-center h-screen space-y-4">
  <h1 class="text-white text-3xl font-bold text-center p-8">
    🧠 Mental Health Support LLM 🧠
  </h1>
  <SectionWrapper>
    <BotReply></BotReply>
  </SectionWrapper>
  <SectionWrapper>
    <UserRequest></UserRequest>
  </SectionWrapper>
  <SectionWrapper>
    <div class="flex justify-center">
      <button
        class="p-3 border border-gray-600 rounded-md bg-gray-800 text-gray-100 w-24 focus:outline-none focus:ring-2 focus:ring-blue-400"
        on:click={sendMessage}
        disabled={isLoading}
      >
        <!-- To change to loading icon on the send button-->
        {#if isLoading}
          <svg
            class="animate-spin h-5 w-5 text-white mx-auto"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        {/if}
        {!isLoading ? "Send" : ""}
      </button>
    </div>
  </SectionWrapper>
</div>
