import { FaRobot } from "react-icons/fa";
import ReactMarkdown from "react-markdown";

const AiMessage = ({ message }) => {
  return (
    <div className="flex items-start">
      <div className="w-10 h-10  flex justify-center mx-2">
        <FaRobot className="w-8 h-8" />
      </div>
      <div className="ml-3 p-3 rounded-lg bg-slate-600">
        <p className="text-sm ">
          <div>
            <div className="text-white prose overflow-auto lg:prose-lg">
              <ReactMarkdown>{message}</ReactMarkdown>
            </div>
          </div>
        </p>
      </div>
    </div>
  );
};

export default AiMessage;
