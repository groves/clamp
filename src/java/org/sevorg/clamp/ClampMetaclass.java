package org.sevorg.clamp;

import org.python.core.ArgParser;
import org.python.core.Py;
import org.python.core.PyDictionary;
import org.python.core.PyJavaType;
import org.python.core.PyNewWrapper;
import org.python.core.PyObject;
import org.python.core.PyStringMap;
import org.python.core.PyTuple;
import org.python.core.PyType;
import org.python.core.PyUserType;
import org.python.expose.ExposedNew;
import org.python.expose.ExposedType;

@ExposedType(name = "clamp.Clamper", base = PyJavaType.class, isBaseType = false)
public class ClampMetaclass extends PyType {
    public ClampMetaclass ()
    {
        super(PyType.TYPE);
    }

    @ExposedNew
    public final static PyObject clamp___new__(PyNewWrapper new_,
                                               boolean init,
                                               PyType subtype,
                                               PyObject[] args,
                                               String[] keywords) {
        ArgParser ap = new ArgParser("type()", args, keywords, "name", "bases", "dict");
        String name = ap.getString(0);
        PyTuple bases = (PyTuple)ap.getPyObjectByType(1, PyTuple.TYPE);
        PyObject dict = ap.getPyObject(2);
        if (!(dict instanceof PyDictionary || dict instanceof PyStringMap)) {
            throw Py.TypeError("type(): argument 3 must be dict, not " + dict.getType());
        }
        dict.__setitem__("__proxymaker__", Py.java2py(ClampMaker.class));
        return new PyUserType(PyType.fromClass(ClampMetaclass.class), name, bases, dict);
    }
}
