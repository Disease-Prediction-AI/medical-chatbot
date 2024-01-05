import { CiUser } from "react-icons/ci";

const UserMessage = ({ message }) => {
  return (
    <div className="flex items-end justify-end">
      <div className="bg-blue-500 p-3 rounded-lg">
        <p className="text-sm text-white prose overflow-auto lg:prose-lg">
          {message}
        </p>
      </div>

      <div className="w-10 h-10  flex justify-center mx-2">
        <CiUser className="w-8 h-8" />
      </div>
    </div>
  );
};

export default UserMessage;
