<script lang="ts">
  import { onDestroy } from "svelte";
  import { botReplyStore, userRequestStore } from "../stores/globalStores";

  let userRequest: string; // This will store the bot's response

  // Subscribe to the store
  const unsubscribe = userRequestStore.subscribe(value => {
    userRequest = value;
  });

  // Automatically update the store when userRequest changes
  $: userRequestStore.set(userRequest);

  // Cleanup the subscription on component destruction
  onDestroy(() => {
    unsubscribe();
  });
</script>

<div class="bg-gray-800 p-4 rounded-lg shadow-lg flex flex-col space-y-4">
  <textarea
    id="userRequest"
    bind:value={userRequest}
    rows="3"
    class="w-full p-3 border border-gray-600 rounded-md bg-gray-900 text-gray-100 focus:outline-none"
    placeholder="Message Bot"
  ></textarea>
</div>
