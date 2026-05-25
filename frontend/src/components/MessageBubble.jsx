function MessageBubble({
  message
}) {

  const isUser =
    message.sender === "user";

  return (

    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >

      <div
        className={`max-w-[70%] p-4 rounded-xl ${
          isUser
            ? "bg-black text-white"
            : "bg-white border"
        }`}
      >

        <div className="whitespace-pre-wrap">

          {message.text}

        </div>

        {/* SOURCES */}
        {!isUser &&
          message.sources &&
          message.sources.length > 0 && (

          <div className="mt-4">

            <p className="font-semibold mb-2">

              Sources

            </p>

            <div className="space-y-2">

              {message.sources.map(
                (source, index) => (

                <div
                  key={index}
                  className="bg-gray-100 p-2 rounded text-sm"
                >

                  <div>
                    {source.source}
                  </div>

                  {source.page && (

                    <div>
                      Page: {source.page}
                    </div>
                  )}

                  {source.sheet && (

                    <div>
                      Sheet: {source.sheet}
                    </div>
                  )}

                  {source.slide && (

                    <div>
                      Slide: {source.slide}
                    </div>
                  )}

                </div>
              ))}

            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default MessageBubble;