<script>
  import BotReply from "../components/BotReply.svelte";
  import SectionWrapper from "../components/SectionWrapper.svelte";
  import UserRequest from "../components/UserRequest.svelte";
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
      >
        Send
      </button>
    </div>
  </SectionWrapper>
</div>
