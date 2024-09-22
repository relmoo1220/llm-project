<script>
  export let userRequest = ""; // This will store the bot's response
</script>

<div class="bg-gray-800 p-4 rounded-lg shadow-lg flex flex-col space-y-4">
  <textarea
    id="userRequest"
    bind:value={userRequest}
    rows="5"
    class="w-full p-3 border border-gray-600 rounded-md bg-gray-900 text-gray-100 focus:outline-none"
    placeholder="Message Bot"
  ></textarea>
</div>
