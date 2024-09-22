<script>
  export let botReply = ""; // This will store the bot's response
</script>

<div class="bg-gray-800 p-4 rounded-lg shadow-lg flex flex-col space-y-4">
  <label for="botReply" class="text-gray-300 font-semibold">Bot's Reply:</label>
  <textarea
    id="botReply"
    bind:value={botReply}
    rows="10"
    class="w-full p-3 border border-gray-600 rounded-md bg-gray-900 text-gray-100 focus:outline-none"
    readonly
  ></textarea>
</div>

