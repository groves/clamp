package org.sevorg.clamp;

import java.lang.reflect.Modifier;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

import org.python.compiler.JavaMaker;
import org.python.core.Py;
import org.python.core.PyObject;
import org.python.core.__builtin__;
import org.python.util.Generic;

public class ClampMaker extends JavaMaker
{
    protected boolean proxyNeeded;

    protected Map<String, PyObject> methodsToAdd = Generic.map();

    public ClampMaker (Class<?> superclass, Class<?>[] interfaces, String pythonClass,
            String pythonModule, PyObject pythonClassDict)
    {
        super(superclass, interfaces, pythonClass, pythonModule,
            pythonModule + "." + pythonClass, pythonClassDict);
        PyObject clampAttr = Py.newString("_clamp");
        System.out.println("Looking for methods to add on " + pythonClass);
        for (PyObject pykey : dict.asIterable()) {
            String key = Py.tojava(pykey, String.class);
            if (key.equals("__init__")) {
                continue;
            }
            PyObject value = dict.__finditem__(key);
            PyObject clampObj = __builtin__.getattr(value, clampAttr, Py.None);
            if (clampObj == Py.None) {
                continue;
            }

            proxyNeeded = true;
            methodsToAdd.put(key, clampObj);
        }
    }

    @Override
    public boolean isProxyNeeded ()
    {
        return super.isProxyNeeded() || proxyNeeded;
    }

    @Override
    public void addConstructors ()
        throws Exception
    {
        // TODO Auto-generated method stub
        super.addConstructors();
//        if '__init__' in dict and hasattr(dict['__init__'], '_clamp'):
//            info = dict['__init__']._clamp
//            for combo in info.argtypes:
//                builder.addConstructor(combo, info.throws)
    }

    @Override
    protected Set<MethodDescr> addMethods ()
        throws Exception
    {
        Set<MethodDescr> added = super.addMethods();
        for (Entry<String, PyObject> meth: methodsToAdd.entrySet()) {
            PyObject clampObj = meth.getValue();
            Class<?> returnClass = Py.tojava(clampObj.__getattr__("returntype"), Class.class);
            Class<?>[] thrownClasses = Py.tojava(clampObj.__getattr__("throws"), Class[].class);
            for (PyObject parameterTypes : clampObj.__getattr__("argtypes").asIterable()) {
                Class<?>[] parameterClasses = Py.tojava(parameterTypes, Class[].class);
                if (added.add(new MethodDescr(meth.getKey(), returnClass, parameterClasses,
                    thrownClasses, Access.PUBLIC))) {
                    addMethod(meth.getKey(), returnClass, parameterClasses, thrownClasses,
                        Modifier.PUBLIC);
                }
            }
        }
        return added;
    }
}
