<script lang="ts">
  import { onDestroy } from "svelte";
  import { botReplyStore, isLoadingStore } from "../stores/globalStores";

  const apiUrl = "http://127.0.0.1:5000";
  let botReply: string;

  // Subscribe to the store
  const unsubscribeBotReplyStore = botReplyStore.subscribe((value) => {
    botReply = value;
  });

  // Cleanup the subscription on component destruction
  onDestroy(() => {
    unsubscribeBotReplyStore();
  });

  async function handleGetHelp() {
    try {
      isLoadingStore.set(true);
      const response = await fetch(apiUrl + "/emergency-resources", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Check if the response is OK (status code 200)
      if (!response.ok) {
        isLoadingStore.set(false);
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }

      // Parse the JSON response
      const data = await response.json();
      console.log("API Response:", data);
      botReply = data.response;
      isLoadingStore.set(false);
    } catch (error) {
      console.error("Error fetching data from Flask API:", error);
    }
  }

  async function handleStatus() {
    try {
      isLoadingStore.set(true);
      const response = await fetch(apiUrl + "/status", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Check if the response is OK (status code 200)
      if (!response.ok) {
        isLoadingStore.set(false);
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }

      // Parse the JSON response
      const data = await response.json();
      console.log("API Response:", data);
      botReply = data.message;
      isLoadingStore.set(false);
    } catch (error) {
      console.error("Error fetching data from Flask API:", error);
    }
  }
</script>

<div class="bg-gray-800 p-4 rounded-lg shadow-lg flex flex-col space-y-4">
  <label for="botReply" class="text-gray-300 font-semibold">Bot's Reply:</label>
  <textarea
    id="botReply"
    bind:value={botReply}
    rows="8"
    class="w-full p-3 border border-gray-600 rounded-md bg-gray-900 text-gray-100 focus:outline-none"
    readonly
  ></textarea>
</div>
<div class="mt-2">
  <button
    class="p-3 border border-gray-600 rounded-md bg-gray-800 text-gray-100 w-[250px] focus:outline-none focus:ring-2 focus:ring-blue-400"
    on:click={handleGetHelp}>Where to reach out for help?</button
  >
  <button
    class="p-3 border border-gray-600 rounded-md bg-gray-800 text-gray-100 w-[180px] focus:outline-none focus:ring-2 focus:ring-blue-400"
    on:click={handleStatus}>Check bot's status</button
  >
</div>
