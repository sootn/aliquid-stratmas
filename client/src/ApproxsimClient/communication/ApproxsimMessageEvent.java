package ApproxsimClient.communication;

/**
 * This class represents the events that may be sent by a ApproxsimMessage to indicate the progress of the message. Events are currently sent
 * when the message is sent to the server, when the client has received the answer and when the answer is handled or when something has gone
 * wrong.
 * 
 * @version 1, $Date: 2006/03/22 14:30:49 $
 * @author Per Alexius
 */
public class ApproxsimMessageEvent extends java.util.EventObject {

    /**
	 * 
	 */
    private static final long serialVersionUID = 6947032622503947818L;

    /**
     * Constructor
     * 
     * @param source The source of the event, i.e. the ApproxsimMessage that generated the event.
     */
    public ApproxsimMessageEvent(ApproxsimMessage source) {
        super(source);
    }

    /**
     * Gets the message that generated this event.
     * 
     * @return The message that generated this event.
     */
    public ApproxsimMessage getMessage() {
        return (ApproxsimMessage) getSource();
    }
}
