<pre>
<%! 
import json
%>
${json.dumps(page)|n}
% for m in menus:
${json.dumps(m)|n}
%endfor
</pre>