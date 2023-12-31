import { useState, useEffect, useRef } from "react";
import AiMessage from "./AiMessage";
import UserMessage from "./UserMessage";

function App() {
  const [conversation, setConversation] = useState({ conversation: [] });
  const [userMessage, setUserMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const lastMessageRef = useRef();
  useEffect(() => {
    const fetchConversation = async () => {
      const conversationId = localStorage.getItem("conversationId");
      if (conversationId) {
        const response = await fetch(
          `/api/conversation/${conversationId}`
        );
        const data = await response.json();
        if (!data.error) {
          setConversation(data);
        }
      }
    };

    fetchConversation();
  }, []);

  useEffect(() => {
    if (lastMessageRef.current) {
      if (lastMessageRef.current) {
        lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
      }
    }
  }, [conversation.conversation]);

  const generateConversationId = () =>
    "_" + Math.random().toString(36).slice(2, 11);

  const handleInputChange = (event) => {
    setUserMessage(event.target.value);
  };

  

  const handleSubmit = async () => {
    if(!userMessage){
      return;
    }
    setIsLoading(true);
    let conversationId = localStorage.getItem("conversationId");
    if (!conversationId) {
      conversationId = generateConversationId();
      localStorage.setItem("conversationId", conversationId);
    }

    const newConversation = [
      ...conversation.conversation,
      { role: "user", content: userMessage },
    ];
    setConversation({ conversation: newConversation });
    setUserMessage("");
    const response = await fetch(
      `/api/conversation/${conversationId}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation: newConversation }),
      }
    );

    const data = await response.json();
    setConversation(data);
    setIsLoading(false);
  };

  const messages =
    conversation?.conversation?.filter(
      (message) => message.role !== "system"
    ) || [];

  return (
    <div className="min-h-screen items-center justify-center bg-black text-white">
      <div className=" min-w-full h-screen max-w-md rounded-lg flex flex-col justify-between shadow-md p-4">
        <div className="flex items-center mb-4">
          <div className="ml-3">
            <p className="text-xl font-medium">
              Medical Assisstant
            </p>
            <p className="text-gray-500">Online</p>
          </div>
        </div>

        <div className="space-y-4 h-full overflow-y-scroll p-5">
          {messages.length > 0 &&
            messages.map((message, index) => (
              <div
                key={index}
                ref={index === messages.length - 1 ? lastMessageRef : null}
              >
                {message.role === "user" ? (
                  <UserMessage message={message.content} />
                ) : (
                  <AiMessage message={message.content} />
                )}
              </div>
            ))}
        </div>

        <div className="mt-4 flex items-center">
          <input
            type="text"
            value={userMessage}
            onChange={handleInputChange}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                event.preventDefault();
                handleSubmit();
              }
            }}
            placeholder={isLoading ? "Processing..." : "Type your message..."}
            className="flex-1 py-2 px-3 rounded-full bg-black text-white focus:outline-none"
          />
          <button
            disabled={isLoading}
            onClick={handleSubmit}
            className={`${isLoading ? "bg-gray-500":"bg-blue-500"} text-white px-4 py-2 rounded-full ml-3 hover:bg-blue-600`}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
