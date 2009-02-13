package org.sevorg.clamp;

import java.lang.reflect.Constructor;

public class Reflector
{
    public static Object instantiate (Class<?> c)
        throws Exception
    {
        return instantiate(c, new Class[0], new Object[0]);
    }

    public static Object instantiate (Class<?> c, Class<?>[] paramTypes, Object[] args)
        throws Exception
    {
        Constructor<?> structor = c.getConstructor(paramTypes);
        return structor.newInstance(args);
    }

    public static Object call (Object o, String methodName)
        throws Exception
    {
        return call(o, methodName, new Class[0], new Object[0]);
    }

    public static Object call (Object o, String methodName, Class<?>[] paramTypes, Object[] args)
        throws Exception
    {
        return o.getClass().getMethod(methodName, paramTypes).invoke(o, args);
    }

    public static Class[] getExceptionTypes (Class c, String methodName, Class<?>[] paramTypes)
        throws Exception
    {
        return c.getMethod(methodName, paramTypes).getExceptionTypes();
    }

}
