package org.sevorg.clamp;

public class Reflector
{
    public static Object instantiate (Class<?> c)
        throws Exception
    {
        return c.newInstance();
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

}
